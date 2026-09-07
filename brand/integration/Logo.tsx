type LogoProps = {
  theme?: 'light' | 'dark';
  variant?: 'horizontal' | 'stacked' | 'symbol' | 'wordmark';
  assetBase?: string;
  className?: string;
  width?: number;
};
const dimensions = {
  horizontal: [1720, 450], stacked: [1280, 860],
  symbol: [512, 512], wordmark: [1220, 245],
} as const;

export function ChainmakersLogo({ theme = 'light', variant = 'horizontal',
  assetBase = '/brand', className, width = 240 }: LogoProps) {
  const color = theme === 'dark' ? 'reverse' : 'color';
  const [w, h] = dimensions[variant];
  return <img
    src={`${assetBase.replace(/\/$/, '')}/svg/${variant}/chainmakers-${variant}-${color}.svg`}
    alt="Chainmakers" width={width} height={width * h / w}
    className={className} style={{ display: 'block', maxWidth: '100%', height: 'auto' }}
  />;
}
