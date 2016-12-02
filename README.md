
## Split line Sublime Plugin ##

Using `ctrl+shift+\` or the context menu option split a single-line array into multiple lines. Developed for `Python` but can be used with any comma-seperated array.

#Examples#

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

# Becomes
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
