const fs = require('fs');
const path = require('path');
const { v4: uuidv4 } = require('uuid');

const DATA_FILE = path.join(__dirname, '../../data/users.json');

const readUsers = () => {
  if (!fs.existsSync(DATA_FILE)) return [];
  return JSON.parse(fs.readFileSync(DATA_FILE));
};

const writeUsers = (data) => {
  fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
};

// @desc    Register a new user
// @route   POST /api/v1/auth/register
exports.register = (req, res) => {
  const { name, email, password, role } = req.body;
  const users = readUsers();

  if (users.find(u => u.email === email)) {
    return res.status(400).json({ message: 'User already exists' });
  }

  const newUser = {
    id: uuidv4(),
    name,
    email,
    password, // Note: We should hash this in production!
    role: role || 'user', // 'user', 'volunteer', 'admin'
    createdAt: new Date().toISOString()
  };

  users.push(newUser);
  writeUsers(users);

  res.status(201).json({
    id: newUser.id,
    name: newUser.name,
    email: newUser.email,
    role: newUser.role,
    token: 'mock-jwt-token-' + newUser.id // Mock token for now
  });
};

// @desc    Login user
// @route   POST /api/v1/auth/login
exports.login = (req, res) => {
  const { email, password } = req.body;
  const users = readUsers();

  const user = users.find(u => u.email === email && u.password === password);

  if (user) {
    res.json({
      id: user.id,
      name: user.name,
      email: user.email,
      role: user.role,
      token: 'mock-jwt-token-' + user.id
    });
  } else {
    res.status(401).json({ message: 'Invalid email or password' });
  }
};
