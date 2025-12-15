module.exports = {
  testEnvironment: 'node',
  testMatch: ['**/backend/**/*.spec.js', '**/backend/**/*.test.js'],
  coverageDirectory: 'coverage',
  collectCoverageFrom: [
    'backend/**/*.js',
    '!backend/**/*.spec.js',
    '!backend/**/*.test.js'
  ],
}
