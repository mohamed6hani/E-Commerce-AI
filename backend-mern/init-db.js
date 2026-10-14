const { db } = require('./db');
db.close((error) => {
  if (error) {
    console.error(error.message);
    process.exitCode = 1;
  }
});
