**01version:**基本功能完成
----------------------
**02version:**
  因为使用for event in pygame.event.get():。当一帧内获取多个改变direction的操作时，会出现蛇头已经del，但是新蛇头没有写入的情况。
  这时碰撞检测代码会被错误地绕过，导致实际上没问题的操作被检测为碰撞到了身体，举例而言当向→时，快速地按下↓←或者快速地按下↑←，会
  导致碰撞发生。
  最初为for event in pygame.event.get():每一个direction的if语句添加了break，即只允许改变一次方向，但是这样蛇的反应就很迟钝，所以可以使用一个list按顺序保存所有得到的direction，但是每次while的总循环只取第一个direction，这样即保证了不会出现冲突的判断，也保证了反应灵敏。
