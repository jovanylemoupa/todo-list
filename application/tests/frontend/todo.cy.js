describe('Todo App E2E Tests', () => {
  beforeEach(() => {
    // Visiter l'application avant chaque test
    cy.visit('/')
  })

  it('devrait charger la page d\'accueil', () => {
    // Vérifier que la page se charge correctement
    cy.contains('Todo').should('be.visible')
  })

  it('devrait pouvoir ajouter une tâche', () => {
    // Trouver le champ d'entrée et ajouter une tâche
    cy.get('input[type="text"]').type('Ma nouvelle tâche')
    cy.get('button').contains('Ajouter').click()

    // Vérifier que la tâche apparaît dans la liste
    cy.contains('Ma nouvelle tâche').should('be.visible')
  })

  it('devrait pouvoir marquer une tâche comme complétée', () => {
    // Ajouter une tâche
    cy.get('input[type="text"]').type('Tâche à compléter')
    cy.get('button').contains('Ajouter').click()

    // Cocher la tâche
    cy.contains('Tâche à compléter').parent().find('input[type="checkbox"]').check()

    // Vérifier que la tâche est marquée comme complétée
    cy.contains('Tâche à compléter').should('have.class', 'completed')
  })

  it('devrait pouvoir supprimer une tâche', () => {
    // Ajouter une tâche
    cy.get('input[type="text"]').type('Tâche à supprimer')
    cy.get('button').contains('Ajouter').click()

    // Supprimer la tâche
    cy.contains('Tâche à supprimer').parent().find('button').contains('Supprimer').click()

    // Vérifier que la tâche n'existe plus
    cy.contains('Tâche à supprimer').should('not.exist')
  })
})
