# `mzt`

The `mzt` package contains optimizer tools for Materialize developers.

## Installation (`pyenv`)

We need a Python version higher than `3.9.x`

```bash
PYTHON_VERSION=3.9.5
```

Run the following commands whenever the contents of this folder change:

```bash
# activate mzt environment
pyenv virtualenv-delete mzt
pyenv virtualenv ${PYTHON_VERSION} mzt

# install package
pyenv activate mzt
pip install .

# install zsh shell completion
echo "$(_MZT_COMPLETE=zsh_source mzt)" > ~/.zfunc/_mzt
rm -f ~/.zcompdump; compinit
```

## Explain Plan Dot Graphs

The `explain` subcommand provides facilities for deriving `*.dot` files from the output of an `EXPLAIN ... PLAN FOR ...` query.
Check the command `--help` for details:

```bash
mzcli explain --help
```

Example:

```bash
mzt explain query raw 'select a, b from (VALUES (1, 2)) AS R(a,b)'
```

Output:

```bash
digraph G {
    node0 [shape = record, label=" CallTable wrap2(1, 2)\l"]
}
```

## Explain Plan Repositories

The `explain repository` subcommand provides an interface for curating repositories of dot graphs for `EXPLAIN ... PLAN FOR ...` outputs.
Check the command `--help` for details:

```bash
mzcli explain repository --help
```

Example:

```bash
# set repository location 
# the value given here is used as default if the envvar
# or the --repository option are not present
export MZT_REPOSITORY="$HOME/mzt-repos/default"

# initialize repository and add some queries
mzt explain repository add 'select a, b from (VALUES (1, 2)) AS R(a,b)'
mzt explain repository add 'select b, a from (VALUES (1, 2)) AS R(a,b)'

# start a server to browse the repository
python -m http.server --directory "$MZT_REPOSITORY" 7123 > /dev/null 2>&1 &
```

The repository will be then available at http://localhost:7123/index.xml.

## Useful Snippets

To add pretty-printed queries, write the query in a `$TEMP_FILE` and then run:

```bash
mzt explain repository add "$(cat $TEMP_FILE)"
```

To update all images in an existing repository:

```bash
for f in $(find $MZT_REPOSITORY -name 'query.sql'); do 
    mzt explain repository add "$(cat $f)";
done
```

To delete all images in an existing repository:

```bash
for f in $(find $MZT_REPOSITORY -name 'query.sql'); do 
    mzt explain repository remove "$(cat $f)";
done
```
