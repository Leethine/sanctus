package CatalogueUtils;

use strict;
use warnings;
use Digest::MD5::File qw( file_md5_hex );

my $LEVEL = 1;

# Read catalogue file, return a hash
sub _read_cat_file {
  my $filename = shift;
  my %result;

  open(FH, '<', $filename) or die "Failed to open catalogue file: $filename";
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

# Read catalogue file, return a hash, ignore missing fields
sub _read_cat_file_ignore_missing {
  my $filename = shift;
  my %result = _read_cat_file($filename);
  for (keys %result) {
    delete($result{$_}) if ($result{$_} eq "");
  }
  return %result;
}

# Write (override) a specific field of a catalogue file
# Ignore if key does not exist
# arg1: key, arg2: new value, arg3: filename
sub _write_cat_file_field {
  my $key = shift;
  my $newval = shift;
  my $filename = shift;
  die "Wrong number of arguments" if !defined $key or !defined $newval or !defined $filename;

  my %result = _read_cat_file($filename);
  return if !exists($result{$key});

  open(FH, '<', $filename) or die "Failed to open $filename";
  my @lines = <FH>;
  close($filename);
  my $newline = qq/$key: $newval\n/;
  open(FH, '>', $filename) or die "Failed to open $filename";
  foreach (@lines) {
    if ($_ =~ /^$key\s*\:/) {
      print FH $newline;
    } else {
      print FH $_;
    }
  }
  close($filename);
}

# Get md5 of a file
# arg1: filename
# arg2: length to chop from the string
sub _get_file_md5 {
  my $filename = shift;
  my $chopped = shift;
  my $md5 = file_md5_hex($filename) or die "Failed to obtain md5sum of: $filename";
  return substr($md5, 0, $chopped) if (defined $chopped);
  return $md5;
}

# Assert the validity of insertion/update/delete type
sub _assert_type {
  my $type = shift;
  unless ($type ~~ ["composer", "piece", "collection", "arrangement", "template"]) {
    die "Type $type not valid";
  }
}

# Verify catalogue file, return false if not valid 
# arg1: filepath, arg2: type
sub _verify_catalogue_file {
  my $filename = shift;
  my $type = shift;

  my $status = 0;
  my %catalogue = _read_cat_file_ignore_missing($filename);
  if ($type eq "composer") {
    $status = exists($catalogue{'LastName'}) and exists($catalogue{'FirstName'});
  }
  else {
    $status = exists($catalogue{'Title'});
  }
  return $status;
}

1;