import pico2d
import logo_state
import play_state
import title_state

pico2d.open_canvas(1300, 600)
states = [logo_state, title_state, play_state]
for state in states:
    state.enter()
# game main loop code
    while state.running:
        state.handle_events()
        state.update()
        state.draw()

    state.exit()

# finalization code
pico2d.close_canvas()