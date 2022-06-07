import random

from enemies import TankEnemy
from enemies import FastEnemy

class Wave:
    def __init__(self):
        self.waveTime = 0
        self.tankEnemies = 1
        self.fastEnemies = 2

        self.inBetweenWaves = False

    def Start(self, wave):
        tankEnemies = []
        for i in range(wave[self.tankEnemies]):
            enemySpawnTime = random.randint(0 * 10, wave[self.waveTime] * 10) / 10
            tankEnemy = TankEnemy(enemySpawnTime)
            tankEnemies.append(tankEnemy)

        fastEnemies = []
        for i in range(wave[self.fastEnemies]):
            enemySpawnTime = random.randint(0 * 10, wave[self.waveTime] * 10) / 10
            fastEnemy = FastEnemy(enemySpawnTime)
            fastEnemies.append(fastEnemy)

        return tankEnemies, fastEnemies
