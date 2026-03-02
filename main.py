from math import sin, cos, radians
import altair as alt
import pandas as pd
import streamlit as st
import random


class Print_Iface:
    def plot_trajectory(self, xs, ys, title="Trajectory"):
        if not xs:
            st.warning("No trajectory points were generated.")
            return

        df = pd.DataFrame({"x": xs, "y": ys})

        max_x = max(xs) if xs else 0
        max_y = max(ys) if ys else 0
        x_max = max(200, (int(max_x / 10) + 1) * 10)
        y_max = max(100, (int(max_y / 10) + 1) * 10)

        st.subheader(title)

        chart = (
            alt.Chart(df)
            .mark_line()
            .encode(
                x=alt.X("x:Q", scale=alt.Scale(domain=[0, x_max]), title="Distance (m)"),
                y=alt.Y("y:Q", scale=alt.Scale(domain=[0, y_max]), title="Height (m)")
            )
            .properties(width=700, height=400)
        )
        st.altair_chart(chart, use_container_width=True)


class Cannonball:
    def __init__(self, x, printer=None):
        self._x = x
        self._y = 0
        self._vx = 0
        self._vy = 0
        self.printer = printer if printer is not None else Print_Iface()

    def move(self, sec, grav):
        dx = self._vx * sec
        dy = self._vy * sec
        self._vy = self._vy - grav * sec
        self._x = self._x + dx
        self._y = self._y + dy

    def getX(self):
        return self._x

    def getY(self):
        return self._y

    def shoot(self, angle, velocity, user_grav, step=0.1, title="Trajectory"):
        self._vx = velocity * cos(angle)
        self._vy = velocity * sin(angle)

        xs = []
        ys = []

        while True:
            self.move(step, user_grav)
            if self.getY() <= 0:
                break
            xs.append(self.getX())
            ys.append(self.getY())

        self.printer.plot_trajectory(xs, ys, title=title)
        return xs, ys


class Crazyball(Cannonball):
    def __init__(self, x, printer=None):
        super().__init__(x, printer=printer)
        self.rand_q = 0

    def move(self, sec, grav):
        super().move(sec, grav)
        self.rand_q = random.randrange(0, 10)
        if self.getX() < 400 and self.getY() > 0:
            jitter = (self.rand_q - 4.5) * 0.25
            self._x += jitter
            self._y += jitter * 0.6


def run_app():
    st.title("Cannonball Trajectory")

    angle_deg = st.number_input(
        "Starting angle (degrees)", min_value=0.0, max_value=90.0, value=45.0
    )
    velocity = st.selectbox("Initial velocity", options=[15, 25, 40], index=1)

    gravity_options = {"Earth": 9.81, "Moon": 1.62}
    gravity_name = st.selectbox("Gravity", options=list(gravity_options.keys()), index=0)
    gravity = gravity_options[gravity_name]

    step = 0.1

    col1, col2 = st.columns(2)
    simulate = col1.button("Simulate")
    simulate_crazy = col2.button("Simulate Crazy")

    if simulate or simulate_crazy:
        angle_rad = radians(angle_deg)
        printer = Print_Iface()

        if simulate_crazy:
            ball = Crazyball(0, printer=printer)
            title = f"Crazy Trajectory ({gravity_name} gravity)"
        else:
            ball = Cannonball(0, printer=printer)
            title = f"Normal Trajectory ({gravity_name} gravity)"

        ball.shoot(angle_rad, velocity, gravity, step, title=title)


if __name__ == "__main__":
    run_app()
