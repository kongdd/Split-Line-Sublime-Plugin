
#Split Line Sublime Plugin#

Using `ctrl+shift+\` (``ctrl+shift+` `` for OSX) or the context menu option split a single-line array into multiple lines. Developed for `Python` but can be used with any comma-seperated array.

Turn recursive splitting on/off through the sublime-settings file for the plugin.

##Examples##

```python
array = [1, 2, 3, 4, 5,]

# Becomes
array = [
	1,
	2,
	3,
	4,
	5,
]
```

```python
array = (1, 2, {3, 4}, 5,)

# Normally:
array = (
	1,
	2,
	{3, 4},
	5,
)

# With recursive_split = true:
array = (
	1,
	2,
	{
		3,
		4,
	},
	5,
)
```

```python
def my_function(a, b, c):
	pass

# Becomes
def my_function(
	a,
	b,
	c
):
	pass
```

##Installation##

Clone this repo into your sublime `Packages` folder.

###Linux###

```
cd ~/.config/sublime-text-3/Packages/
git clone https://github.com/stevebasher/Split-Line-Sublime-Plugin.git
```

###OSX###

```
cd ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/
git clone https://github.com/stevebasher/Split-Line-Sublime-Plugin.git
```
