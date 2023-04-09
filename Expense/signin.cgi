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
my $password = $cgi->param('password');

# open(my $fh, '<', 'customertest.txt') or die "Could not open file $!";

# while (my $row = <$fh>) {
#   chomp $row;
#   ($name, $password) = split(':', $row);
# }

# close($fh);
#print "Content-type:text/html\r\n\r\n";

# Prepare the SQL statement to check if the cust_id and password exist in the customer table
my $sth = $dbh->prepare("SELECT * FROM signup WHERE name = ? AND password = ?");

# Execute the SQL statement with the cust_id and password values
$sth->execute($name, $password);

# Fetch the results of the SQL statement
my $row = $sth->fetchrow_arrayref;

# Check if the form has been submitted and the cust_id and password exist in the customer table
if ($row) {
  # Login successful, redirect to the homepage
  # Open the file for writing
  open(my $fh, '>', 'customer.txt') or die "Cannot open file: $!";

  # Write the cust_id and password to the file
  print $fh "$name:$password\n";

  # Close the file
  close($fh);
    print $cgi->redirect('/Expense/navigate.html');
} else {
  # Login failed, display an error message
  print $cgi->redirect('/Expense/register.html?msg=Invalid customer ID or password');
}

# Disconnect from the database
$dbh->disconnect;