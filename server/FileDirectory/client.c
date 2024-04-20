#include <stdlib.h>
#include <stdio.h>
#include "csapp.h"

// For all parameters passed into the program (fname, lname, zip code, department, salary)
#define MAXELEMENT 1024

#define MAX_HOST 16
#define MAXINPUT 2

int query_user(int);
void read_response(int, const char *);
void add_record(int);
void name_search(int);
void zip_code_search(int);
void salary_search(int);
void terminate(int);

int main(int argc, char * argv[])
{
    char * hostname;
    char * portnum;
    int port, clientfd;
    int rv = 1; 
    // Ensure user passes in hostname and port only
    if (argc != 3)
    {
        printf("Please include a hostname and port\n");
        return 1; 
    }

    hostname = argv[1];
    portnum = argv[2];

    // Check the port number
    // Since we use IPv4, the max is 16 bit unsigned int
    port = atoi(argv[2]);
    if (port < 1 || port > 65535)
    {
        printf("Please check your port number and try again (1-65535)\n");
        return 1; 
    }

    // wrapper calls getadderinfo, socket, and connect functions
    clientfd = Open_clientfd(hostname, portnum); 
   
    // Check the client file descriptor
    if (clientfd < 0)
    {
        printf("There has been an error connecting to hostname: %s port: %d. Aborting!\n", hostname, port);
        return 1;
    } 

    /*
        rv stands for return value. 
        In this case 1 = true
                     0 = false
    */
    while(rv == 1)
    {
        rv = query_user(clientfd);
    }
    
    return 0;
}

/*
    Queries what the user wants to do and calls the corresponding function to do the task. 
    Return value (bool): 
        0 = error or user terminated
        1 = success
*/
int query_user(int clientfd)
{
    char input[MAXINPUT];
    int rv = 1;
    int c;
    
    // Show the user their options
    printf("(1) Add record\n");
    printf("(2) Search by Name\n");
    printf("(3) Search by Zip Code\n");
    printf("(4) Search by Salary\n");
    printf("(5) Terminate\n");
    printf("Select an option [1,2,3,4 or 5]: ");
   
    // Get the user's input
    Fgets(input, MAXINPUT, stdin);

    // Clear out input buffer 
    while ((c = getchar()) != '\n' && c != EOF);
  
    // All cases other than terminate print a newline, so it's added into the 
    // switch
    switch(input[0])
    {
        // Add record
        case '1':
            printf("\n");
            add_record(clientfd);
            break;
        // Name search
        case '2':
            printf("\n");
            name_search(clientfd);
            break;
        // Zip Code search
        case '3':
            printf("\n");
            zip_code_search(clientfd);
            break;
        // Salary search
        case '4':
            printf("\n");
            salary_search(clientfd);
            break;
        // Terminate the program
        case '5':
            terminate(clientfd);
            rv = 0;
            break;
        // Do not change rv here to allow query_user to be ran again
        default:
            printf("Error: please insert 1-5 and try again!\n");
    }     

    return rv;
}

/*
    Reads server response and outputs it to the terminal
    inputs: 
        client file descriptor to chat with the server
        string stating the function's name that is calling read_response
    
    If the read is unsuccessful, the program exits
*/
void read_response(int clientfd, const char * function_name)
{
    char buffer[MAXLINE];
    size_t n;

    bzero(buffer, MAXLINE);
    
    n = read(clientfd, buffer, MAXLINE);

    if (n < 0)
    {
        printf("%s: an error has occured while reading from the server. Aborting!", function_name);
        exit(1);
    }

    printf("Message From Server:\n%s\n", buffer); 
   
    return;
}
/*
    Gets the inputs from the user to send to the server.
    Tries to create a record based on user input
*/
void add_record(int clientfd)
{

    // TO DO: Change MAXLINE/5 to something ..... better (sprintf complains)
    char buffer[MAXLINE], first_name[MAXELEMENT], last_name[MAXELEMENT],
         zip_code[MAXELEMENT], department[MAXELEMENT], salary[MAXELEMENT];
    size_t n;
    
    bzero(buffer, MAXLINE);
    
    // Get input to send to server
    printf("Enter First Name: ");
    Fgets(first_name, MAXELEMENT, stdin); 

    printf("Enter Last Name: ");
    Fgets(last_name, MAXELEMENT, stdin); 

    printf("Enter Zip Code: ");
    Fgets(zip_code, MAXELEMENT, stdin); 
    
    printf("Enter Department: ");
    Fgets(department, MAXELEMENT, stdin); 
    
    printf("Enter Salary: ");
    Fgets(salary, MAXELEMENT, stdin);  
    

    // Remove the newline characters from each element:
    first_name[strcspn(first_name, "\n")] = 0;
    last_name[strcspn(last_name, "\n")] = 0;
    zip_code[strcspn(zip_code, "\n")] = 0;
    department[strcspn(department, "\n")] = 0;
    salary[strcspn(salary, "\n")] = 0;


    // Combine the inputs together to send to the server.
    // 1 denotes we are trying to add a record
    snprintf(buffer, MAXLINE, "1,%s,%s,%s,%s,%s", first_name, last_name, zip_code, department, salary); 
  
    n = write(clientfd, buffer, MAXLINE);
    if (n < 0)
    {
        printf("add_record(): There was an error writing to the server. Aborting!\n");
        exit(1);
    }
    
    // Output server response
    read_response(clientfd, "add_record()");

    return;
}
void name_search(int clientfd)
{
    char buffer[MAXLINE], first_name[MAXELEMENT], last_name[MAXELEMENT];
    size_t n;
    
    bzero(buffer, MAXLINE);
    
    // Get input to send to server
    printf("Enter First Name: ");
    Fgets(first_name, MAXELEMENT, stdin); 

    printf("Enter Last Name: ");
    Fgets(last_name, MAXELEMENT, stdin); 
    
    // Remove the newline characters from each element:
    first_name[strcspn(first_name, "\n")] = 0;
    last_name[strcspn(last_name, "\n")] = 0;

    
    // Combine the inputs together to send to the server.
    // 2 denotes we are trying to search by name
    snprintf(buffer, MAXLINE, "2,%s,%s", first_name, last_name); 
    
    n = write(clientfd, buffer, MAXLINE);
    if (n < 0)
    {
        printf("name_search(): There was an error writing to the server. Aborting!\n");
        exit(1);
    }
    
    // Output server response
    read_response(clientfd, "name_search()");

    return;
}
void zip_code_search(int clientfd)
{
    char buffer[MAXLINE], zip_code[MAXELEMENT];
    size_t n;
    
    bzero(buffer, MAXLINE);
    
    // Get input to send to server
    printf("Enter Zip Code: ");
    Fgets(zip_code, MAXELEMENT, stdin); 
    
    // Remove the newline characters from each element:
    zip_code[strcspn(zip_code, "\n")] = 0;
    
    // Combine the inputs together to send to the server.
    // 2 denotes we are trying to search by zip code
    snprintf(buffer, MAXLINE, "3,%s", zip_code); 
    
    n = write(clientfd, buffer, MAXLINE);
    if (n < 0)
    {
        printf("zip_code_search(): There was an error writing to the server. Aborting!\n");
        exit(1);
    }
    
    // Output server response
    read_response(clientfd, "zip_code_search()");
    
    return;
}
void salary_search(int clientfd)
{
    char buffer[MAXLINE], salary[MAXELEMENT], operator[MAXELEMENT];
    size_t n;
    
    bzero(buffer, MAXLINE);
    
    // Get input to send to server
    printf("Enter Salary: ");
    Fgets(salary, MAXELEMENT, stdin); 

    printf("Enter Comparison Type [’>’,’<’,’==’,’>=’,’<=’]: ");
    Fgets(operator, MAXELEMENT, stdin); 
    
    // Remove the newline characters from each element:
    salary[strcspn(salary, "\n")] = 0;
    operator[strcspn(operator, "\n")] = 0;

    
    // Combine the inputs together to send to the server.
    // 4 denotes we are trying to search by salary
    snprintf(buffer, MAXLINE, "4,%s,%s", operator, salary); 
    
    n = write(clientfd, buffer, MAXLINE);
    if (n < 0)
    {
        printf("salary_search(): There was an error writing to the server. Aborting!\n");
        exit(1);
    }
    
    // Output server response
    read_response(clientfd, "salary_search()");
    
    return;
}

/*
    Closes the connection to the server by sending the value "5".
*/
void terminate(int clien