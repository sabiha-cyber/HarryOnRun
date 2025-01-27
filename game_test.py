import pytest
import pygame
from game import collision,coin_collision,obstacle_movement

def test_collision():
    player = pygame.Rect (300,200,50,50)
    obstacle = [pygame.Rect(300,200,20,20)]
    assert collision(player,obstacle) == False

def test_no_collision():
    player = pygame.Rect(300, 200, 50, 50)
    obstacle = [pygame.Rect(100, 100, 20, 20)]
    assert collision(player,obstacle) == True
def test_coin_collision():
    global coins
    coins = 0 
    player = pygame.Rect(300, 200, 50, 50)
    coin = [pygame.Rect(290, 200, 20, 20),pygame.Rect(100, 100, 20, 20) ]
    coin_collision(player,coin) 
    assert coins == 1
    assert len(coin) == 1


def test_obstacle_movement():
    obstacle = [pygame.Rect(290, 200, 20, 20),pygame.Rect(-110, 100, 20, 20) ]
    updated_obstacles = obstacle_movement(obstacle)
    assert len(updated_obstacles) == 1  
    assert updated_obstacles[0].x == 285 
