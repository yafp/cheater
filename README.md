cheater
=====
`cheater` allows you to create and view interactive cheatsheets on the
command-line. It was designed to help remind \*nix system administrators of
options for commands that they use frequently, but not frequently enough to
remember.

![The obligatory xkcd](http://imgs.xkcd.com/comics/tar.png 'The obligatory xkcd')


Example
-------
The next time you're forced to disarm a nuclear weapon without consulting
Google, you may run:

```sh
cheater tar
```

You will be presented with a cheatsheet resembling:

```sh
# To extract an uncompressed archive: 
tar -xvf '/path/to/foo.tar'

# To extract a .gz archive:
tar -xzvf '/path/to/foo.tgz'

# To create a .gz archive:
tar -czvf '/path/to/foo.tgz' '/path/to/foo/'

# To extract a .bz2 archive:
tar -xjvf '/path/to/foo.tgz'

# To create a .bz2 archive:
tar -cjvf '/path/to/foo.tgz' '/path/to/foo/'
```

To see what cheatsheets are available, run `cheater -l`.

Note that, while `cheater` was designed primarily for \*nix system administrators,
it is agnostic as to what content it stores. If you would like to use `cheater`
to store notes on your favorite cookie recipes, feel free.


Installing
----------
First, install the dependencies:

```sh
[sudo] pip install docopt pygments appdirs
```

Then clone this repository:
```sh
git clone git@github.com:yafp/cheater.git
```

Lastly, `cd` into the cloned directory, then run:

```sh
[sudo] python setup.py install
```



Modifying Cheatsheets
---------------------
The value of `cheater` is that it allows you to create your own cheatsheets - the
defaults are meant to serve only as a starting point, and can and should be
modified.

Cheatsheets are stored in the `~/.cheater/` directory, and are named on a
per-keyphrase basis. In other words, the content for the `tar` cheatsheet lives
in the `~/.cheater/tar` file.

Provided that you have a `CHEAT_EDITOR`, `VISUAL`, or `EDITOR` environment
variable set, you may edit cheatsheets with:

sh
cheater -e foo
```

If the `foo` cheatsheet already exists, it will be opened for editing.
Otherwise, it will be created automatically.

After you've customized your cheatsheets, I urge you to track `~/.cheater/` along
with your dotfiles.


Configuring
-----------

### Setting a DEFAULT_CHEAT_DIR ###
Personal cheatsheets are saved in the `~/.cheater` directory by default, but you
can specify a different default by exporting a `DEFAULT_CHEATER_DIR` environment
variable:

```sh
export DEFAULT_CHEATER_DIR='/path/to/my/cheats'
```

### Setting a CHEATERPATH ###
You can additionally instruct `cheater` to look for cheatsheets in other
directories by exporting a `CHEATERPATH` environment variable:

```sh
export CHEATERPATH='/path/to/my/cheats'
```

You may, of course, append multiple directories to your `CHEATERPATH`:

```sh
export CHEATERPATH="$CHEATERPATH:/path/to/more/cheats"
```

You may view which directories are on your `CHEATERPATH` with `cheater -d`.

### Enabling Syntax Highlighting ###
`cheater` can optionally apply syntax highlighting to your cheatsheets. To enable
syntax highlighting, export a `CHEATERCOLORS` environment variable:

```sh
export CHEATERCOLORS=true
```

#### Specifying a Syntax Highlighter ####
You may manually specify which syntax highlighter to use for each cheatsheet by
wrapping the sheet's contents in a [Github-Flavored Markdown code-fence][gfm].

Example:

<pre>
```sql
-- to select a user by ID
SELECT *
FROM Users
WHERE id = 100
```
</pre>

If no syntax highlighter is specified, the `bash` highlighter will be used by
default.



Credits
-----------
`cheater` is a fork of [Chris Allen Lane](https://github.com/chrisallenlane)'s wonderful project `cheat`.

Please check it out: [https://github.com/chrisallenlane/cheat](https://github.com/chrisallenlane/cheat)
