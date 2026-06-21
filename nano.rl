world(500, 500)

r1.init(122, 12)
r2.init(250, 250)
r3.init(80, 180)
r4.init(300, 40)

# r1.movX(150)
r1.movY(150)
r1.movX(220)
r1.movY(80)

r2.movY(200)
r2.movX(100)

r3.movX(30)
r3.movX(200)

r4.movX(192)
r4.movY(202)

r1.say("Hello World!")
r4.say("I am here too.")

r1.patrol(10)

var x = r2.getPos()
var y = x.x
show(x.x)
show(x.y)

result()