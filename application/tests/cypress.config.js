const { defineConfig } = require('cypress')

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:5173', // URL de votre application Vue.js
    specPattern: 'frontend/**/*.cy.{js,jsx,ts,tsx}',
    supportFile: 'frontend/support/e2e.js',
    fixturesFolder: 'frontend/fixtures',
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },
})
