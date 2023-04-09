#!C:\xampp\perl\bin\perl.exe
use CGI qw(:standard);
use DBI;
print header();
my $cgi = CGI->new;

# connect to database 
my $dbh = DBI->connect("dbi:mysql:database=expense_db;host=localhost", "root", "");

# handle database connection error
if (!$dbh) {
    die("Error connecting to database: " . DBI->errstr);
}
# handle form submission
if (param()) {
    my $name = $cgi->param('name');
    my $gender = $cgi->param('gender');
    my $totmeb = $cgi->param('totmeb');
    my $mobile = $cgi->param('mobile');
    my $salarydate = $cgi->param('salarydate');
    my $address = $cgi->param('address');
    my $occupation = $cgi->param('occupation');
    my $salary = $cgi->param('salary');
    my $grocery = $cgi->param('grocery');
    my $maintanence = param('maintanence');
    my $emi = $cgi->param('emi');
    my $fuel = $cgi->param('fuel');
    my $savings = $cgi->param('savings');
    my $others = $cgi->param('others');

    # insert data into database
    my $sth = $dbh->prepare("INSERT INTO personal_details (name, gender, totmeb, mobile, salarydate, address, occupation, salary, grocery, maintanence, emi, fuel, savings, others) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)");
    my $result = $sth->execute($name, $gender, $totmeb, $mobile, $salarydate, $address, $occupation, $salary, $grocery, $maintanence, $emi, $fuel, $savings, $others);

    # handle database insertion error
    if (!$result) {
        my $link = "<link rel='stylesheet' href='https://fonts.googleapis.com/css2?family=Poppins&display=swap'>";
        print $link;
        print "<p style='color:red; left:0;margin-top:-100px;position:absolute;font-weight:bold;font-size:20px;font-family:Poppins;display:flex;align-item:center;top: 50%;width: 100%;justify-content:center;'>Error inserting data into database: " . $dbh->errstr . "</p>";
    } else {
        my $link = "<link rel='stylesheet' href='https://fonts.googleapis.com/css2?family=Poppins&display=swap'>";
        print $link;
        print "<p style='color:green; left:0;margin-top:-100px;position:absolute;font-weight:bold;font-size:20px;font-family:Poppins;display:flex;align-item:center;top: 50%;width: 100%;justify-content:center;'>Data stored in the database successfully.</p>";
        
        # add "View Expenses" button
        print "<div style='display: flex; align-items: center; justify-content: center; height: 100vh;'>
            <a id='view-expenses' href='viewsummary.cgi'>View Expenses</a>
        </div>";

        # add the style for the "View Expenses" button
        print "<style>
            #view-expenses {
                background-color: #4CAF50;
                border-radius: 4px;
                color: white;
                display: block;
                font-family: Poppins;
                font-size: 18px;
                margin: 0 auto;
                padding: 14px 20px;
        text-align: center;
        text-decoration: none;
        width: 200px;
    }
    #view-expenses:hover {
        background-color: #2E8B57;
        cursor: pointer;
    }
</style>"
    }
}
