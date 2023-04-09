#!C:\xampp\perl\bin\perl.exe
use CGI qw(:standard);
use DBI;

print header();

# connect to database 
my $dbh = DBI->connect("dbi:mysql:database=expense_db;host=localhost", "root", "");

# handle database connection error
if (!$dbh) {
    die("Error connecting to database: " . DBI->errstr);
}

my $filename = 'customer.txt';
open(my $fh, '<', $filename) or die "Could not open file '$filename' $!";

while (my $row = <$fh>) {
  chomp $row;
  ($name, $password) = split(':', $row);
}

close($fh);

# retrieve data from the database
my $sth = $dbh->prepare("SELECT  name, salarydate, salary, grocery, maintanence, emi, fuel, savings, others FROM personal_details where name = ?");
$sth->execute($name);

# display the data in a table format
print "<html>";
print "<head>";
print "<title>Expense Report</title>";
print "<link rel='stylesheet' href='https://fonts.googleapis.com/css2?family=Poppins&display=swap'>";
print "<link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'/>";
print "<style>";
print "body { font-family: 'Poppins', sans-serif; }";
print "table { border-collapse: collapse; width: 100%; }";
print "th, td { text-align: center; padding: 8px; }";
print "th { background-color: rgb(56, 122, 255); color: white; }";
print "tr:nth-child(even) { background-color: #f2f2f2; }";
print ".fa-check {color: green;}";
print ".fa-times {color: red;}";
print "</style>";
print "</head>";
print "<body>";
print "<h1 style='display:flex;align-item:center;justify-content:center;'>YOUR EXPENSES<h1/>";
print "<table border='1'>";
print "<tr><th>Name</th><th>Salary Date</th><th>Salary</th><th>Grocery</th><th>Maintenance</th><th>EMI</th><th>Fuel</th><th>Savings</th><th>Others</th><th>Tallied</th></tr>";

while (my $row = $sth->fetchrow_hashref()) {
    $salary = $row->{salary};
    $grocery = $row->{grocery};
    $maintanence = $row->{maintanence};
    $emi = $row->{emi};
    $fuel = $row->{fuel};
    $savings = $row->{savings};
    $others = $row->{others};
    $tick = "";
    if($salary == $grocery+$maintanence+$emi+$fuel+$savings+$others){
      $tick = "<i class='fas fa-check'></i>"; # HTML for tick icon
    }else{
      $tick = "<i class='fas fa-times'></i>"; # HTML for cross icon

    }
    print "<tr>";
    print "<td>$row->{name}</td>";
    print "<td>$row->{salarydate}</td>";
    print "<td>$row->{salary}</td>";
    print "<td>$row->{grocery}</td>";
    print "<td>$row->{maintanence}</td>";
    print "<td>$row->{emi}</td>";
    print "<td>$row->{fuel}</td>";
    print "<td>$row->{savings}</td>";
    print "<td>$row->{others}</td>";
    print "<td>$tick</td>";
    print "</tr>";

}
print "</table>";
print "<p style='background-color: #ffffff;display:flex;align-item:center;justify-content:center;'><a href='./edit.html'><button style='font-family: Poppins, sans-serif;width:150px;background-color: #4CAF50; color: white;font-size:20px; padding: 8px 20px; border: none; border-radius: 4px;'>Edit</button></a></p>";
print "<p style='background-color: #ffffff;display:flex;align-item:center;justify-content:center;'><a href='./delete.html'><button style='font-family: Poppins, sans-serif;width:150px;background-color: #f44336; color: white;font-size:20px; padding: 8px 20px; border: none; border-radius: 4px;'>Delete</button></a></p>";

print "<p style='background-color: #ffffff;display:flex;align-item:center;justify-content:center; '>
<a href='logout.cgi'>
  <button style='background-color: #4CAF50; color: white; padding: 8px 20px; border: none; border-radius: 4px;font-family: Poppins, sans-serif;width:150px;font-size:20px;'>LogOut</button>
</a>
</p>"; 

print "</body>";
print "</html>";

# disconnect from the database
$dbh->disconnect();
