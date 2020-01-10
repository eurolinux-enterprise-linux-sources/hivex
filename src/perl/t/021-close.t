# hivex Perl bindings -*- perl -*-
# Copyright (C) 2010 Red Hat Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

use strict;
use warnings;
use Test::More tests => 2;

use Win::Hivex;

my $srcdir = $ENV{srcdir} || ".";

# Put it in a block so the handle gets destroyed as well.
{
    my $h = Win::Hivex->open ("$srcdir/../images/minimal");
    ok ($h);
}
ok (1);
