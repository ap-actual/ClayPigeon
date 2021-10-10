# Clay Pigeon 

## utils
### pull ticks
Pull ticks will either pull ticks from yfinance, normalize them, and save them locally into .csv's or will read that local data into the program. 

### Normalize Ticks
Will normalize ticks into the following structure

| idx | 0    | 1     | 2    | 3    | 4   | 5    | 6     | 7     | 8    | 9      |
|-----|------|-------|------|------|-----|------|-------|-------|------|--------|
| var | Year | Week# | Day# | High | Low | Open | Close | %High | %Low | %Close |
