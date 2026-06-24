// 은행 로고/표시명 매핑 파일
// 위치: frontend/src/constants/bankLogoMap.js
// 사용 예:
//   import { getBankLogo, getBankDisplayName } from '@/constants/bankLogoMap'
//   const logo = getBankLogo('주식회사 케이뱅크')
//   const name = getBankDisplayName('주식회사 케이뱅크') // '케이뱅크'

export const BANK_LOGO_FILES = {
  woori: new URL('../assets/banks/commercial/woori.svg', import.meta.url).href,
  sc: new URL('../assets/banks/commercial/sc.png', import.meta.url).href,
  shinhan: new URL('../assets/banks/commercial/shinhan.svg', import.meta.url).href,
  kb: new URL('../assets/banks/commercial/kb.svg', import.meta.url).href,
  hana: new URL('../assets/banks/commercial/hana.svg', import.meta.url).href,
  citi: new URL('../assets/banks/commercial/citi.svg', import.meta.url).href,
  im: new URL('../assets/banks/commercial/im.svg', import.meta.url).href,
  busan: new URL('../assets/banks/local/busan.svg', import.meta.url).href,
  gyeongnam: new URL('../assets/banks/local/gyeongnam.svg', import.meta.url).href,
  gwangju: new URL('../assets/banks/local/gwangju.svg', import.meta.url).href,
  jeonbuk: new URL('../assets/banks/local/jeonbuk.svg', import.meta.url).href,
  jeju: new URL('../assets/banks/local/jeju.svg', import.meta.url).href,
  ibk: new URL('../assets/banks/policy/ibk.svg', import.meta.url).href,
  kdb: new URL('../assets/banks/policy/kdb.svg', import.meta.url).href,
  post: new URL('../assets/banks/policy/post.svg', import.meta.url).href,
  nh: new URL('../assets/banks/cooperative/nh.svg', import.meta.url).href,
  suhyup: new URL('../assets/banks/cooperative/suhyup.svg', import.meta.url).href,
  mg: new URL('../assets/banks/cooperative/mg.svg', import.meta.url).href,
  shinhyup: new URL('../assets/banks/cooperative/shinhyup.svg', import.meta.url).href,
  sbi: new URL('../assets/banks/savings/sbi.svg', import.meta.url).href,
  kakao: new URL('../assets/banks/internet/kakao.svg', import.meta.url).href,
  toss: new URL('../assets/banks/internet/toss.svg', import.meta.url).href,
  kbank: new URL('../assets/banks/internet/kbank.svg', import.meta.url).href,
}

const BANK_DEFINITIONS = [
  {
    key: 'woori',
    name: '우리은행',
    category: 'commercial',
    aliases: ['우리은행', '주식회사 우리은행', 'WOORI', 'Woori Bank'],
  },
  {
    key: 'sc',
    name: 'SC제일은행',
    category: 'commercial',
    aliases: ['SC제일은행', 'SC제일', '스탠다드차타드은행', '한국스탠다드차타드은행', 'Standard Chartered'],
  },
  {
    key: 'shinhan',
    name: '신한은행',
    category: 'commercial',
    aliases: ['신한은행', '주식회사 신한은행', 'SHINHAN', 'Shinhan Bank'],
  },
  {
    key: 'kb',
    name: 'KB국민은행',
    category: 'commercial',
    aliases: ['KB국민은행', '국민은행', '주식회사 국민은행', 'KB', 'Kookmin'],
  },
  {
    key: 'hana',
    name: 'KEB하나은행',
    category: 'commercial',
    aliases: ['KEB하나은행', '하나은행', '주식회사 하나은행', 'HANA', 'Hana Bank'],
  },
  {
    key: 'citi',
    name: '시티은행',
    category: 'commercial',
    aliases: ['시티은행', '한국씨티은행', 'Citibank Korea', 'Citi', 'Citibank'],
  },
  {
    key: 'im',
    name: 'iM뱅크',
    category: 'commercial',
    aliases: ['iM뱅크', 'IM뱅크', '아이엠뱅크', '주식회사 아이엠뱅크', 'iM Bank', 'IM Bank', '대구은행', 'DGB대구은행', '주식회사 대구은행', 'DGB', 'Daegu'],
  },
  {
    key: 'busan',
    name: '부산은행',
    category: 'local',
    aliases: ['부산은행', 'BNK부산은행', '주식회사 부산은행', 'Busan Bank'],
  },
  {
    key: 'gyeongnam',
    name: '경남은행',
    category: 'local',
    aliases: ['경남은행', 'BNK경남은행', '주식회사 경남은행', 'Gyeongnam Bank'],
  },
  {
    key: 'gwangju',
    name: '광주은행',
    category: 'local',
    aliases: ['광주은행', '주식회사 광주은행', 'KJB', 'Gwangju Bank'],
  },
  {
    key: 'jeonbuk',
    name: '전북은행',
    category: 'local',
    aliases: ['전북은행', 'JB전북은행', '주식회사 전북은행', 'Jeonbuk Bank'],
  },
  {
    key: 'jeju',
    name: '제주은행',
    category: 'local',
    aliases: ['제주은행', '주식회사 제주은행', 'Jeju Bank'],
  },
  {
    key: 'ibk',
    name: 'IBK기업은행',
    category: 'policy',
    aliases: ['IBK기업은행', '기업은행', '중소기업은행', 'IBK', 'Industrial Bank of Korea'],
  },
  {
    key: 'kdb',
    name: 'KDB산업은행',
    category: 'policy',
    aliases: ['KDB산업은행', '산업은행', '한국산업은행', 'KDB', 'Korea Development Bank'],
  },
  {
    key: 'post',
    name: '우체국',
    category: 'policy',
    aliases: ['우체국', '우체국예금', 'Post Office'],
  },
  {
    key: 'nh',
    name: 'NH농협은행',
    category: 'cooperative',
    aliases: ['NH농협은행', '농협은행', '농협은행주식회사', '농협은행 주식회사', '농협', '농협중앙회', 'NH', 'NongHyup'],
  },
  {
    key: 'suhyup',
    name: '수협은행',
    category: 'cooperative',
    aliases: ['수협은행', '수협', '수산업협동조합중앙회', 'Suhyup'],
  },
  {
    key: 'mg',
    name: 'MG새마을금고',
    category: 'cooperative',
    aliases: ['MG새마을금고', '새마을금고', 'MG'],
  },
  {
    key: 'shinhyup',
    name: '신협',
    category: 'cooperative',
    aliases: ['신협', '신용협동조합', '신용협동조합중앙회', 'CU'],
  },
  {
    key: 'sbi',
    name: 'SBI저축은행',
    category: 'savings',
    aliases: ['SBI저축은행', 'SBI'],
  },
  {
    key: 'kakao',
    name: '카카오뱅크',
    category: 'internet',
    aliases: ['카카오뱅크', '주식회사 카카오뱅크', '카카오뱅크 주식회사', '카뱅', 'KakaoBank', 'Kakao Bank', 'kakaobank'],
  },
  {
    key: 'toss',
    name: '토스뱅크',
    category: 'internet',
    aliases: ['토스뱅크', '주식회사 토스뱅크', '토스뱅크 주식회사', '토스은행', 'TossBank', 'Toss Bank', 'tossbank'],
  },
  {
    key: 'kbank',
    name: '케이뱅크',
    category: 'internet',
    aliases: ['케이뱅크', '주식회사 케이뱅크', '케이뱅크 주식회사', 'K뱅크', '케이은행', 'Kbank', 'K Bank', 'kbank'],
  },
]

export const BANK_LOGO_LIST = BANK_DEFINITIONS.map((bank) => ({
  key: bank.key,
  name: bank.name,
  category: bank.category,
  logo: BANK_LOGO_FILES[bank.key],
}))

export const BANK_LOGOS = BANK_DEFINITIONS.reduce((acc, bank) => {
  bank.aliases.forEach((alias) => {
    acc[alias] = BANK_LOGO_FILES[bank.key]
  })
  acc[bank.name] = BANK_LOGO_FILES[bank.key]
  return acc
}, {})

export const BANK_DISPLAY_NAMES = BANK_DEFINITIONS.reduce((acc, bank) => {
  bank.aliases.forEach((alias) => {
    acc[alias] = bank.name
  })
  acc[bank.name] = bank.name
  return acc
}, {})

export function normalizeBankName(bankName) {
  return String(bankName || '')
    .trim()
    .replace(/㈜|\(주\)|주식회사|은행주식회사/g, '')
    .replace(/\s+/g, '')
    .replace(/[()\[\]{}.,·ㆍ_-]/g, '')
    .toLowerCase()
}

function findBankDefinition(bankName) {
  if (!bankName) return null

  const raw = String(bankName).trim()
  const exactHit = BANK_DEFINITIONS.find((bank) => {
    return bank.name === raw || bank.aliases.includes(raw)
  })

  if (exactHit) return exactHit

  const normalized = normalizeBankName(raw)
  if (!normalized) return null

  const candidates = BANK_DEFINITIONS.flatMap((bank) => {
    const names = [bank.name, ...bank.aliases]
    return names.map((name) => ({
      bank,
      normalizedName: normalizeBankName(name),
    }))
  })
    .filter((item) => item.normalizedName)
    .sort((a, b) => b.normalizedName.length - a.normalizedName.length)

  const partialHit = candidates.find((item) => {
    return normalized.includes(item.normalizedName) || item.normalizedName.includes(normalized)
  })

  return partialHit?.bank || null
}

export function getBankKey(bankName) {
  return findBankDefinition(bankName)?.key || null
}

export function getBankLogo(bankName) {
  const key = getBankKey(bankName)
  return key ? BANK_LOGO_FILES[key] : null
}

export function getBankDisplayName(bankName) {
  const bank = findBankDefinition(bankName)
  return bank?.name || String(bankName || '').trim()
}
