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
# check if search button has been clicked and retrieve input date
my $search_date = param('search');
$search_date = "" if !$search_date;

# retrieve data from the database based on search input
my $sth;
if ($search_date) {
    $sth = $dbh->prepare("SELECT  name, salarydate, salary, grocery, maintanence, emi, fuel, savings, others FROM personal_details where name = ? AND salarydate = ?");
    $sth->execute($name, $search_date);
} else {
    $sth = $dbh->prepare("SELECT  name, salarydate, salary, grocery, maintanence, emi, fuel, savings, others FROM personal_details where name = ?");
    $sth->execute($name);
}

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
print ".fa-check {color: green;font-size:30px;}";
print ".fa-times {color: red;font-size:30px;}";
print "html,
body {
  scroll-behavior: smooth;
}
::-webkit-scrollbar {
  width: 8px; /* width of the scrollbar */
}

::-webkit-scrollbar-track {
  background-color: #f1f1f1; /* color of the track */
}

::-webkit-scrollbar-thumb {
  background-color: #1100ff95; /* color of the scrollbar thumb */
  border-radius: 4px; /* roundness of the scrollbar thumb */
}

::-webkit-scrollbar-thumb:hover {
  background-color: #797886; 
}";
print ".searchbtn { background-color: blue;
color: white;
padding: 6px 10px; 
border: none;
border-radius: 100px; 
font-family: Poppins, sans-serif;
width: 80px; 
font-size: 15px;}";
print ".searchdate {display:flex;align-item:center;justify-content:center;padding: 15px;border-radius: 0.5rem;width: 15%;border: none;outline: none;background: hsla(260, 100%, 44%, 0.1);font-family: Poppins, sans-serif;margin-bottom: 1rem;}";
print ".formarea{ display:flex;align-item:center;justify-content:center;gap:25px; }";
print "</style>";
print "</head>";
print "<body>";
print "<h1 style='display:flex;align-item:center;justify-content:center;font-size:40px;'>YOUR EXPENSES<h1/>";
print "<form method='post' action='' class='formarea'>";
print "<label for='search'style='font-size:25px;'>Search by Date:</label>";
print "<input type='date' id='search' name='search' value='$search_date' class='searchdate'>";
print "<i style='padding-top:7px;'><input type='submit' value='Search' class='searchbtn'></i>";
print "</form>";
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
print"<div style='background-color: #ffffff;display:flex;justify-content:center;align-items:center; gap:20px;padding-bottom:20px;'>
<a href='./edit.html'><button style='font-family: Poppins, sans-serif;width:150px;background-color: #4CAF50; color: white;font-size:20px; padding: 8px 20px; border: none; border-radius: 4px;'>Edit</button></a>
<a href='./delete.html'><button style='font-family: Poppins, sans-serif;width:150px;background-color: #f44336; color: white;font-size:20px; padding: 8px 20px; border: none; border-radius: 4px;'>Delete</button></a>
<a href='getdetails.html'><button style='background-color: #4CAF50; color: white; padding: 8px 20px; border: none; border-radius: 4px;font-family: Poppins, sans-serif;width:150px;font-size:20px;'>Add New</button></a>
<a href='logout.cgi'><button style='background-color: red; color: white; padding: 8px 20px; border: none; border-radius: 4px;font-family: Poppins, sans-serif;width:150px;font-size:20px;'>LogOut</button></a>
</div>";
print "</body>";
print "</html>";

# disconnect from the database
$dbh->disconnect();
