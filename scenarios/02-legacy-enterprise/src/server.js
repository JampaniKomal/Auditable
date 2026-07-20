const fs = require('fs');
const path = require('path');
const express = require('express');
const cors = require('cors');
const mysql = require('mysql2/promise');
const winston = require('winston');

const logDir = path.join(__dirname, 'logs');
fs.mkdirSync(logDir, { recursive: true });

const auditLogger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.printf(({ timestamp, level, message }) => `${timestamp} - ${level.toUpperCase()} - ${message}`)
  ),
  transports: [
    new winston.transports.File({ filename: path.join(logDir, 'legacy_audit.log') }),
    new winston.transports.Console()
  ]
});

const app = express();
app.use(cors());
app.use(express.json());

const DB_HOST = process.env.DB_HOST || 'localhost';
const DB_PORT = Number(process.env.DB_PORT || '3306');
const DB_NAME = process.env.DB_NAME || 'legacy_bank';
const DB_USER = process.env.DB_USER || 'root';
const DB_PASS = process.env.DB_PASS || 'plaintextroot';
const LEGACY_BACKDOOR_TOKEN = process.env.LEGACY_BACKDOOR_TOKEN || 'LEGACY_MASTER_OVERRIDE_2026';

const pool = mysql.createPool({
  host: DB_HOST,
  port: DB_PORT,
  user: DB_USER,
  password: DB_PASS,
  database: DB_NAME,
  waitForConnections: true,
  connectionLimit: 5
});

async function initializeDatabase() {
  const schema = `
    CREATE TABLE IF NOT EXISTS employee_accounts (
      id INT AUTO_INCREMENT PRIMARY KEY,
      employee_name VARCHAR(100),
      account_number VARCHAR(24),
      card_pan VARCHAR(20),
      temp_password VARCHAR(100)
    )
  `;

  await pool.query(schema);
  const [rows] = await pool.query('SELECT COUNT(*) AS count FROM employee_accounts');

  if (rows[0].count === 0) {
    await pool.query(`
      INSERT INTO employee_accounts (employee_name, account_number, card_pan, temp_password)
      VALUES
      ('Vikram Mehta', 'LEG-0011223344', '4111-1111-1111-1111', 'legacy123'),
      ('Ananya Rao', 'LEG-0099887766', '5500-0000-0000-0004', 'password2026'),
      ('Suresh Iyer', 'LEG-0044556677', '3400-0000-0000-009', 'changeMe!')
    `);
  }

  auditLogger.info('Legacy database initialized with unencrypted financial records.');
}

app.get('/api/health', (request, response) => {
  response.json({ status: 'ok', service: 'legacy-enterprise-api' });
});

app.get('/api/ledger', async (request, response) => {
  const authorization = request.get('authorization');

  if (authorization !== `Bearer ${LEGACY_BACKDOOR_TOKEN}`) {
    auditLogger.warn(`Unauthorized access attempt detected with token: ${authorization}`);
    return response.status(401).json({ detail: 'Unauthorized request profile.' });
  }

  const [rows] = await pool.query('SELECT employee_name, account_number, card_pan, temp_password FROM employee_accounts');
  const responseData = rows.map((row) => ({
    name: row.employee_name,
    account: row.account_number,
    pan: row.card_pan,
    password: row.temp_password
  }));

  auditLogger.info(`Authorized legacy export executed. Raw payload dumped to disk: ${JSON.stringify(responseData)}`);
  response.json({ status: 'success', data: responseData });
});

async function start() {
  await initializeDatabase();
  const port = Number(process.env.PORT || '3000');
  app.listen(port, '0.0.0.0', () => {
    auditLogger.info(`Legacy enterprise API listening on port ${port}.`);
  });
}

start().catch((error) => {
  auditLogger.error(`Fatal startup failure: ${error.message}`);
  process.exit(1);
});
