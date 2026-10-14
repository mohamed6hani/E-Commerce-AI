"""Validate the Node demo with a disposable project/database and stdlib Python."""
import json
from contextlib import closing
import os
from pathlib import Path
import shutil
import socket
import sqlite3
import subprocess
import sys
import tempfile
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def main():
    with tempfile.TemporaryDirectory(prefix='ecommerce-smoke-') as directory:
        temp = Path(directory)
        backend = temp / 'backend-mern'
        shutil.copytree(ROOT / 'backend-mern', backend,
                        ignore=shutil.ignore_patterns('node_modules', 'data', '.env', '*.log'))
        # Local dependencies must precede any unrelated ancestor node_modules.
        shutil.copytree(ROOT / 'backend-mern/node_modules', backend / 'node_modules')
        (temp / 'tools').mkdir()
        (temp / 'docs').mkdir()
        shutil.copy2(ROOT / 'tools/seed_demo_data.py', temp / 'tools/seed_demo_data.py')
        if (ROOT / 'frontend-react/build').is_dir():
            shutil.copytree(ROOT / 'frontend-react/build', temp / 'frontend-react/build')
        with socket.socket() as reservation:
            reservation.bind(('127.0.0.1', 0))
            port = reservation.getsockname()[1]
        env = {**os.environ, 'PORT': str(port)}
        base = f'http://127.0.0.1:{port}'

        def api(path, method='GET', body=None):
            payload = None if body is None else json.dumps(body).encode()
            request = Request(base + path, data=payload, method=method,
                              headers={'Content-Type': 'application/json'})
            with urlopen(request, timeout=5) as response:
                return json.loads(response.read())

        log_path = temp / 'server.log'
        with log_path.open('w') as log:
            server = subprocess.Popen(['node', 'server.js'], cwd=backend, env=env,
                                      stdout=log, stderr=subprocess.STDOUT)
            try:
                deadline = time.monotonic() + 25
                while True:
                    if server.poll() is not None:
                        raise RuntimeError('Server exited: ' + log_path.read_text())
                    try:
                        with urlopen(base + '/api/health', timeout=1) as response:
                            assert response.status == 200
                        break
                    except (URLError, TimeoutError):
                        if time.monotonic() >= deadline:
                            raise RuntimeError('Server did not become ready')
                        time.sleep(0.1)

                def seed():
                    result = subprocess.run([sys.executable, str(temp / 'tools/seed_demo_data.py')],
                                            check=True, capture_output=True, text=True)
                    return json.loads(result.stdout)

                assert api('/api/products') == []
                first = seed()
                assert first['demo_counts'] == {'users': 9, 'products': 12, 'orders': 16,
                                              'order_items': 36, 'reviews': 10}
                assert abs(first['demo_order_value'] - 2047.50) < 0.005
                assert all(value == 0 for value in seed()['inserted'].values())
                products = api('/api/products')
                orders = api('/api/orders')
                assert len(products) == 12 and len(orders) == 16
                for order in orders:
                    assert abs(order['total'] - sum(item['quantity'] * item['price']
                                                   for item in order['items'])) < 0.005
                watch = next(product for product in products if product['title'] == 'Pulse Smartwatch')
                quote = api(f"/api/ai/price?productId={watch['id']}&demandFactor=0.8&competitorPrice=145")
                assert quote['dynamicPrice'] == 154.80
                product = api('/api/products', 'POST', {'title': 'Smoke fixture', 'price': 10, 'stock': 2})
                edited = api(f"/api/products/{product['id']}", 'PUT', {'price': 12, 'stock': 3})
                assert edited['price'] == 12 and edited['stock'] == 3
                api(f"/api/products/{product['id']}", 'DELETE')
                assert len(api('/api/products')) == 12
                try:
                    api('/api/orders', 'POST', {'userId': orders[0]['user_id'],
                                              'items': [{'productId': 999999, 'quantity': 1, 'price': 1}]})
                    raise AssertionError('Invalid foreign key order was accepted')
                except HTTPError as error:
                    assert error.code == 400
                assert len(api('/api/orders')) == 16
                with closing(sqlite3.connect(backend / 'data/ecommerce.sqlite')) as database:
                    assert database.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
                    assert database.execute('PRAGMA foreign_key_check').fetchall() == []
                if (ROOT / 'frontend-react/build').is_dir():
                    with urlopen(base + '/dashboard', timeout=5) as response:
                        assert response.status == 200 and b'<div id="root">' in response.read()
                print('PASS: startup, seed idempotency, counts, order totals, pricing, product CRUD, rollback, SQLite integrity and frontend serving')
            finally:
                server.terminate()
                try:
                    server.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    server.kill()
                    server.wait(timeout=5)


if __name__ == '__main__':
    main()
