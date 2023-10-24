package TextMatching; 

use strict;
use warnings;

# Match composer name, with or without the initials
sub match_composer_name {
  my $firstname_str = lc(shift);
  my $lastname_str = lc(shift);
  my $keyword_str = lc(shift);

  my @keywords = split(" ", "$keyword_str");
  my @firstname = split(" ", $firstname_str);

  my $ismatch = 1;

  # try matching last name
  if ($lastname_str eq $keywords[0]) {
    $ismatch *= 1;
    shift(@keywords);
  } elsif ($lastname_str eq $keywords[-1]) {
    $ismatch *= 1;
    pop(@keywords);
  } else {
    return 0;
  }

  # try matching first name
  if (!@keywords) {
    return $ismatch;
  } else {
    if ($#keywords == $#firstname) {
      for (my $i = 0; $i <= $#keywords; $i++) {
        if ($keywords[$i] =~ /^[a-z]\.$/) {
          my $temp = substr($firstname[$i], 0, 1) . ".";
          $ismatch *= ($temp eq $keywords[$i]);
        } else {
          $ismatch *= ($keywords[$i] eq $firstname[$i]);
        }
      }
    } else {
      return 0;
    }
  }
  return $ismatch;
}

1;