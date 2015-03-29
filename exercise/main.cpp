#include <iostream>



const int map_width = 10;
const int map_height = 5;



class Bullet
{
public:
	Bullet(int gun_pos)
	{
		x = gun_pos;
		y = map_height - 1;
		c = '*';
	}

	void move()
	{
		y++;
	}

	void kill()
	{
		y = map_height;
	}

	bool out_of_bounds()
	{
		return y >= map_height;
	}

	int x, y;
	char c;
};



class Robot
{
public:
	virtual void move()=0;

	bool collides(Bullet other)
	{
		return other.x == x && other.y == y;
	}

	int x, y;
	char c;
};



class Robert : public Robot
{
public:
	Robert(bool is_hard_mode)
	{
		y = x = 1;
		c = is_hard_mode ? 'r' : 'R';
	}

	void move()
	{
		if (x < map_width - 1)
			x++;
	}
};



class Donald : public Robot
{
public:
	Donald(bool is_hard_mode)
	{
		y = 0;
		x = 4;
		c = is_hard_mode ? 'd' : 'D';

		dx = -1;
	}

	void move()
	{
		x += dx;

		if (x >= map_width)
		{
			x = map_width;
			dx = -1;
		}
		else if (x < 0)
		{
			x = 0;
			dx = 1;
		}
	}

	int dx;
};



class Clifford : public Robot
{
public:
	Clifford(bool is_hard_mode)
	{
		y = 3;
		x = 2;
		c = is_hard_mode ? 'c' : 'C';

		timer = 0;
		max_timer = 3;
	}

	void move()
	{
		timer++;

		if (timer >= max_timer)
		{
			//move in a random direction
			timer = 0;
		}
	}

	int timer;
	int max_time;
};



class Player
{
public:
};



class Gun
{
public:
	Gun()
	{
		x = 0;
		bullets_left = 10;
	}

	void update()
	{
		//go through and remove 'dead' bullets
	}

	int x;
	int bullets_left;

	//vector of bullet pointers
};



int main()
{
	Robot * robots[3];
	Player player;

	while(true)
	{

	}

	return 0;
}