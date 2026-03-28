import { Injectable, NotFoundException } from '@nestjs/common';
import { RealtimeGateway } from '../realtime/realtime.gateway';
import { WalletService } from '../wallet/wallet.service';

export type BetStatus = 'pending' | 'win' | 'lose';

export type Bet = {
  id: number;
  userId: number;
  matchId: string;
  odds: number;
  amount: number;
  potentialWin: number;
  status: BetStatus;
};

@Injectable()
export class BettingService {
  private readonly bets = new Map<number, Bet>();
  private id = 1;

  constructor(
    private readonly walletService: WalletService,
    private readonly realtime: RealtimeGateway,
  ) {}

  async placeBet(userId: number, matchId: string, odds: number, amount: number) {
    await this.walletService.withdraw(userId, amount);

    const bet: Bet = {
      id: this.id++,
      userId,
      matchId,
      odds,
      amount,
      potentialWin: Number((amount * odds).toFixed(2)),
      status: 'pending',
    };

    this.bets.set(bet.id, bet);
    this.realtime.sendBetUpdate(userId, bet);
    return bet;
  }

  async settleBet(betId: number, result: 'win' | 'lose') {
    const bet = this.bets.get(betId);
    if (!bet) throw new NotFoundException(`Bet not found: ${betId}`);

    bet.status = result;
    if (result === 'win') {
      await this.walletService.deposit(bet.userId, bet.potentialWin);
    }

    this.realtime.sendBetUpdate(bet.userId, bet);
    return bet;
  }
}
