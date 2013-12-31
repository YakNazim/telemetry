FILES=frontend/src/*.coffee frontend/widgets/*.coffee
STATIC=static/psas/telemetry.js

all: clean build

build:
	coffee -cj $(STATIC) $(FILES)

clean:
	rm -f $(STATIC)*
