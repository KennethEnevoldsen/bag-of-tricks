# Bag of Tricks
Kenneth Enevoldsen personal utility functions. Typically include neat simple functions
implementing efficient tricks.


# Installation
```
pip install git+https://github.com/KennethEnevoldsen/bag-of-tricks
```

# Content

    ├── README.md
    ├── bagoftricks             <- The package
    │   ├── names               <- auto-generate run names
    │   ├── batch               <- generate batch out of iterable
    │   ├── mean_update         <- update/calculate mean from iterable
    │   ├── shuffle_buffer      <- create a shuffle buffer on iterable
    │   └── reapeatable_gen.py  <- make a generator repeatable  
    │

# Usage
```
from bagoftricks.names import create_run_name

create_run_name()
# '2021-10-28-19.55_brainy-mole'
```


---- 
*Note*: This package is not intended to be productionfriendly. If you want to use it in 
production I strongly recommend extracting the desired function.