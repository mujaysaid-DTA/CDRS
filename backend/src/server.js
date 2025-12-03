const app = require('./app');
const dotenv = require('dotenv');

dotenv.config();

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`\n🚀 Backend Server running on port ${PORT}`);
  console.log(`🔗 API URL: http://localhost:${PORT}/api/v1`);
});
