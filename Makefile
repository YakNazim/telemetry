FILES=frontend/src/*.coffee frontend/widgets/*.coffee
STATIC=static/psas/telemetry.js

all: clean build

build:
	cat `find ./frontend/ -name *.css` > static/psas/style.css
	coffee -cj $(STATIC) $(FILES)

clean:
	rm -f $(STATIC)*
