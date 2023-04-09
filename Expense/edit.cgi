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

my $name = "";
my $password = "";
my $salarydate = $cgi->param("salarydate");

    my $salary = $cgi->param('salary');
    my $grocery = $cgi->param('grocery');
    my $maintanence = $cgi->param('maintanence');
    my $emi = $cgi->param('emi');
    my $fuel = $cgi->param('fuel');
    my $savings = $cgi->param('savings');
    my $others = $cgi->param('others');

my $filename = 'customer.txt';
open(my $fh, '<', $filename) or die "Could not open file '$filename' $!";

while (my $row = <$fh>) {
  chomp $row;
  ($name, $password) = split(':', $row);
}

close($fh);

my $sth = $dbh->prepare("SELECT * FROM signup WHERE name = ? AND password = ?");

# Execute the SQL statement with the cust_id and password values
$sth->execute($name, $password);

# Fetch the results of the SQL statement
my $row = $sth->fetchrow_arrayref;

# Check if the form has been submitted and the passwords match
if ($row) {

   # Prepare the SQL statement to retrieve the counts of each product
    my $sth = $dbh->prepare("UPDATE personal_details SET salary=?,grocery=?,maintanence=?,emi=?,fuel=?,savings=?,others=? WHERE name =  ? && salarydate = ?");
    $sth->execute($salary,$grocery,$maintanence,$emi,$fuel,$savings,$others,$name,$salarydate);

    # Redirect to the orderonline.html page with the counts in the URL
    print $cgi->redirect("/Expense/viewsummary.cgi?msg=Update Successful");
    
} else {
    # Redirect the user back to the index page
    print $cgi->redirect('/Expense/register.html?msg=Login to continue');
}

# Disconnect from the database
$dbh->disconnect;