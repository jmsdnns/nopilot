# No Pilot

WOOHOO NO HANDS

## Usage:

Pass the prompt as cli inputs

```
$ nopilot hello world in erlang
io:format("Hello world~n", []).
```

Pipe a prompt via stdin

```
$ echo "hello world in haskell" | nopilot
main = putStrLn "Hello, world!"
```

Type the prompt out with an editor

```
$ nopilot -e  # type 'hello world in c++'
#include <iostream>
using namespace std;

int main() {
    cout << "Hello world" << endl;
    return 0;
}
```

### Same thing, with different models

```
$ nopilot hello world in erlang -m gpt-4o
io:format("hello world~n").
```

```
$ echo "hello world in haskell" | nopilot -m gpt-4
main = putStrLn "Hello, world!"
```

```
$ nopilot -e -m gpt-4o
#include <iostream>
using namespace std;

int main() {
    cout << "Hello world" << endl;
    return 0;
}
```
