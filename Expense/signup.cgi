#!C:\xampp\perl\bin\perl.exe

use strict;
use warnings;
use CGI;
use DBI;

# Connect to MySQL database
my $dsn = "DBI:mysql:database=expense_db;host=localhost";

my $dbh = DBI->connect($dsn, "root", "", { RaiseError => 1 })
    or die "Couldn't connect to database: " . DBI->errstr;
# Retrieve form data
my $cgi = CGI->new;

my $name = $cgi->param('name');
my $email = $cgi->param('email');
my $password = $cgi->param('password');
my $submit = $cgi->param('signup');

#print "Content-type:text/html\r\n\r\n";


    # Check if the customer already exists
    my $sth = $dbh->prepare("SELECT COUNT(*) FROM signup WHERE name = ?");
    $sth->execute($name);
    my ($count) = $sth->fetchrow_array;
    $sth->finish;

    if ($count == 0) {
        # Insert the new customer into the database
        my $sql = "INSERT INTO signup (name, password,email) VALUES (?, ?, ?)";
        my $sth = $dbh->prepare($sql);
        $sth->execute($name, $password,$email);
        $sth->finish;
        $dbh->commit;

        # Show an alert message to the user indicating that the signup was successful
        print $cgi->redirect('/Expense/register.html?msg=Signup successful');
    } else {
        # Show an alert message to the user indicating that the username already exists
        print $cgi->redirect('/Expense/register.html?msg=Username already exists!');
    }

# Disconnect from the database
$dbh->disconnect;