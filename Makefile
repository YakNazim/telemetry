FILES=frontend/src/*.coffee
STATIC=static/psas/

all: clean build

build:
	coffee -c -o $(STATIC) $(FILES)

clean:
	rm -f $(STATIC)*
