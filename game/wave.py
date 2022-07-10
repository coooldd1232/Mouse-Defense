import random

from enemies import FastEnemy

class Wave:
    def __init__(self):
        self.waveTime = 0
        self.fastEnemies = 1

        self.inBetweenWaves = False

    def Start(self, wave):

        fastEnemies = []
        for i in range(wave[self.fastEnemies]):
            enemySpawnTime = random.randint(0 * 10, wave[self.waveTime] * 10) / 10
            fastEnemy = FastEnemy(enemySpawnTime)
            fastEnemies.append(fastEnemy)

        return fastEnemies
