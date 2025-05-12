describe('Logging into the system', () => {
  // Define variables used across tests
  let uid; // User ID
  let name; // Full name of the user
  let email; // Email of the user
  const task = 'Test task'; // Task name

 before(function () {
      // create a fabricated user from a fixture
      cy.fixture('user.json')
        .then((user) => {
          cy.request({
            method: 'POST',
            url: 'http://localhost:5000/users/create',
            form: true,
            body: user
          }).then((response) => {
            uid = response.body._id.$oid
            name = user.firstName + ' ' + user.lastName
            email = user.email
          })
        })

        
    })

  beforeEach(function () {
    // Visit the main page before each test
    cy.visit('http://localhost:3000');
    
    cy.contains('div', 'Email Address')
      .find('input[type=text]')
      .type(email);
    // Submit the form on this page
    cy.get('form')
      .submit();
    // Assert that the user is now logged in
    cy.get('h1')
      .should('contain.text', 'Your tasks, ' + name);
    // Create a task for the user
    cy.contains('div', 'Title')
        .find('input[type=text]')
        .type(task)
    cy.get('form')
      .submit();
  });

    it('R8CU1: Add a todo.', () => {
        // Try to find the task

       cy.get('.container')
        .contains('.title-overlay', task)
        .parent('a')
        .click();



        // Add a todo
        cy.get('.todo-list')
            .find('.inline-form')
            .find('input[type=text]')

            .type('Test todo', { force: true })

        .get('.inline-form input[value="Add"]')
        .click({ force: true });


        // Check so that it was added
        
        cy.get('.todo-list')
            .find('.todo-item')
            .should('contain.text', 'Test todo');
        
    });

    it('R8CU1: Check if add button is disabled when empty', () => {

        // Try to find the task
        cy.get('.container')
        .contains('.title-overlay', task)
        .parent('a')
        .click();

        // Check if it's disabled
        cy.get('.todo-list')
            .find('.inline-form')
            .find('input[type=text]')
            .get('.inline-form input[value="Add"]')
            .should('be.disabled');

        
    })

    it('R8CU2: Toggle todo done.', () => {
        cy.get('.container')
        .contains('.title-overlay', task)
        .parent('a')
        .click();

        



        cy.get('.todo-list .todo-item')
            .first()
            .find('.checker.unchecked')
            .click({ force: true });
        
        // Check so that it was marked as done
        cy.get('.todo-list .todo-item')
            .parent()
            .find('.checker.checked')
            .should('exist');

    })


    it('R8CU2: Toggle todo undone.', () => {
        cy.get('.container')
        .contains('.title-overlay', task)
        .parent('a')
        .click();

        // Mark the todo as done first
        cy.get('.todo-list .todo-item')
            .first()
            .find('.checker.checked')
            .click();

        // Check so that it was marked as not done
        cy.get('.todo-list .todo-item')
            .parent()
            .find('.checker.unchecked')
            .should('exist');
    }
    )

    it('R8CU3: Delete todo.', () => {
        cy.get('.container')
        .contains('.title-overlay', task)
        .parent('a')
        .click();

        // Delete the todo
        cy.get('.todo-list .todo-item')
            .first()
            .find('.remover')
            .click();

        // Check so that it was deleted
        cy.get('.todo-list')
            .find('.todo-item')
            .should('not.exist');
    }
    )

  
        

    


  
    
  

  after(function () {
    // Clean up by deleting the user from the database
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`,
    });
});
  });