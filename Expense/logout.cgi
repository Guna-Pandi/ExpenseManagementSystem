#!C:\xampp\perl\bin\perl.exe

use strict;
use warnings;
use CGI;

my $cgi = CGI->new;
my $filename = 'customer.txt';
# open the file for writing
open(my $fh, '>', $filename) or die "Could not open file '$filename' $!";
# truncate the file
truncate $fh, 0;
# close the file
close $fh;
print $cgi->redirect('/Expense/register.html?msg=Logout successful');
    