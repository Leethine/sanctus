package CatalogueKeeper;

use strict;
use warnings;

my $LEVEL = 1;

# Read catalogue file, return an array
sub _read_cat_file {
  my $filename = shift;
  my %result;

  open(FH, '<', $filename) or die "Failed to open file $filename";
  my @lines;
  while (<FH>) {
    # Ignore hash sign
    push(@lines, $_) if !(substr($_, 0, 1) eq '#') and ($_ =~ m/\w/);
  }
  foreach (@lines) {
    my @pair = split(':', "$_");
    continue if ! @pair;
    my $key = $pair[0] =~ s/\s//gr;
    # trim spaces
    my $val = $pair[1] =~ s/^\s+|\s+$//gr;
    $val =~ s/\s{2,}/ /g;
    # Add to hash if valid
    $result{$key} = $val if ($key ne "");
  }
  return %result;
}

1;