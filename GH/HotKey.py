from pynput.keyboard import Listener, Key, KeyCode
 
store = set()
hot_key = set([Key.alt_l, KeyCode(char='s')])

def handleKeyPress( key ):
    store.add( key )
    print('\x13' in store)
    check = all([True if k in store else False for k in hot_key ])
    print(store)
    print([True if k in store else False for k in hot_key ])
    if check:
        return False # do something
 
def handleKeyRelease( key ): 
    if key in store:
        store.remove( key )
        
    # 종료
    if key == Key.esc:
        return False
 
with Listener(on_press=handleKeyPress, on_release=handleKeyRelease) as listener:
    listener.join()
