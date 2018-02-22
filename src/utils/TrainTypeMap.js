export let SeatTypeMap = {
  '8': 'gg_num',
  '7': 'yb_num',
  'P': '特等座',
  '6': '高级软卧',
  '4': '软卧',
  '3': '硬卧',
  '2': '软座',
  '1': '硬座',
  'F': '动卧',
  '9': '商务座',
  'M': '一等座',
  'O': '二等座',
  'WZ': '无座',
  'MIN': '其他',

  'ANY': '任意',
  'ANYS': '任意卧铺'
}

export default {
  trainTypeMap: {
    'G': '高速',
    'D': '动车',
    'C': '城际',
    'Z': '直达',
    'T': '特快',
    'K': '快速',
    'P': '国际',
    'Y': '旅游',
    'S': '市郊',
    'L': '临时',
    'O': '普通',

    'ANYH': '任意高速列车',
    'ANYO': '任意普通列车'
  },
  highSpeedTrainTypes: new Set(['G', 'D', 'C']),
  ordinaryTrainTypes: new Set(['Z', 'T', 'K', 'P', 'Y', 'S', 'L', 'O']),
  typeForTrain (trainName) {
    var key = trainName.slice(0, 1)
    if (this.trainTypeMap[key] === undefined) key = 'O'
    return key
  },

  seatTypeMap: SeatTypeMap,
  sleeperTypes: new Set(['4', '3', '6', 'F'])
}
