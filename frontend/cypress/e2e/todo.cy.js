
describe('Logging into the system', () => {
  // Define variables used across tests
  let uid; // User ID
  let todoID; // Todo ID
  


    before(function () {
      cy.request({
        method: 'POST',
        url: 'http://localhost:5000/populate',
        form: true,
      })
      .then((response) => {
        console.log("Här är vi nu", response.body);
        uid = response.body.users[0]; // Store the user ID

        
        return cy.request({
          method: 'GET',
          url: `http://localhost:5000/tasks/ofuser/${uid}`,
        });
      })
      .then((response) => {
        console.log("Tasks", response.body);
        todoID = response.body[0]._id.$oid; // Store the todo ID
        console.log("Todo ID:", todoID); // Log the todo ID for debugging

      });
      
    })

    
    

    beforeEach(function () {
      // Visit the main page before each test
      cy.visit('http://localhost:3000');
      
      cy.contains('div', 'Email Address')
        .find('input[type=text]')
        .type("jane.doe@gmail.com");
      // Submit the form on this page
      cy.get('form')
        .submit();
    });

  

      it('R8CU1: Add a todo.', () => {
          // Try to find the task

        cy.get('.container')
          .contains('.title-overlay', 'Improve Devtools')
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

          
          cy.get('.container')
          .contains('.title-overlay', "Improve Devtools")
          .parent('a')
          .click();

          
          try {
              cy.get('.todo-list')
              .find('.inline-form')
              .find('input[type=submit]')
              .should('be.disabled');

          } catch (error) {
              
              cy.log('Error: ' + error.message);
          }
        
      })

      it('R8CU2: Toggle todo done.', () => {
        cy.get('.container')
          .contains('.title-overlay', "Improve Devtools")
          .parent('a')
          .click();

        cy.request({
          method: 'PUT',
          url: `http://localhost:5000/todos/byid/${todoID}`,
          form: true,
          body: {
            data: JSON.stringify({'$set': {'done': false}})
          }
          
        }).then(() => {
          cy.get('.todo-list .todo-item')
            .first()
            .find('.checker')
            .click({ force: true });
            
          
          cy.wait(500)

          
          console.log("todoID som används:", todoID);
          cy.request({
            method: 'GET',
            url: `http://localhost:5000/todos/byid/${todoID}`,
            form: true,
          }).then((response) => {
            console.log("här är loggen", response);
            expect(response.status).to.eq(200); // Check if the todo is marked as done
            
          });
        });
      });


      it('R8CU2: Toggle todo undone.', () => {
          cy.get('.container')
          .contains('.title-overlay', "Improve Devtools")
          .parent('a')
          .click();

          cy.request({
            method: 'PUT',
            url: `http://localhost:5000/todos/byid/${todoID}`,
            form: true,
            body: {
              data: JSON.stringify({'$set': {'done': true}})
            }
          });

          // Check so that it was marked as not done
          cy.get('.todo-list .todo-item')
              .parent()
              .find('.checker.unchecked')
              .should('exist');

          cy.request({
            method: 'GET',
            url: `http://localhost:5000/todos/byid/${todoID}`,
          }).then((response) => {
            expect(response.status).to.eq(200);
          });
      }
      )

      it('R8CU3: Delete todo.', () => {
          cy.get('.container')
          .contains('.title-overlay', "Improve Devtools")
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
              .should('not.contain.text', 'Watch video');
          cy.request({
            method: 'GET',
            url: `http://localhost:5000/todos/byid/${todoID}`,
          }).then((response) => {
            expect(response.status).eq(200); // Check if the todo is deleted
          });
      }
      )

    
    after(function () {
    
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    }).then((response) => {
      // status code 200 means the user was deleted successfully
      // Log the response for debugging (it works)
      console.log("användare",response.body)
    })
  })
});