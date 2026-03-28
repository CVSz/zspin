import { Injectable, NotFoundException } from '@nestjs/common';
import { RealtimeGateway } from '../realtime/realtime.gateway';

type Wallet = { userId: number; balance: number };

@Injectable()
export class WalletService {
  private readonly wallets = new Map<number, Wallet>([
    [1, { userId: 1, balance: 100 }],
    [2, { userId: 2, balance: 70 }],
    [3, { userId: 3, balance: 20 }],
  ]);

  constructor(private readonly realtime: RealtimeGateway) {}

  async deposit(userId: number, amount: number) {
    const wallet = this.ensureWallet(userId);
    wallet.balance += amount;
    this.realtime.sendBalanceUpdate(userId, wallet.balance);
    return wallet;
  }

  async withdraw(userId: number, amount: number) {
    const wallet = this.ensureWallet(userId);
    wallet.balance -= amount;
    this.realtime.sendBalanceUpdate(userId, wallet.balance);
    return wallet;
  }

  async getBalance(userId: number): Promise<number> {
    return this.ensureWallet(userId).balance;
  }

  private ensureWallet(userId: number): Wallet {
    const wallet = this.wallets.get(userId);
    if (!wallet) {
      throw new NotFoundException(`Wallet not found for user ${userId}`);
    }
    return wallet;
  }
}
