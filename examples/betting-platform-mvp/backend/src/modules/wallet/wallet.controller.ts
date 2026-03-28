import { Body, Controller, Get, Param, ParseIntPipe, Post } from '@nestjs/common';
import { IsNumber, Min } from 'class-validator';
import { WalletService } from './wallet.service';

class AmountDto {
  @IsNumber()
  @Min(1)
  amount!: number;
}

@Controller('wallet')
export class WalletController {
  constructor(private readonly walletService: WalletService) {}

  @Post(':userId/deposit')
  deposit(
    @Param('userId', ParseIntPipe) userId: number,
    @Body() body: AmountDto,
  ) {
    return this.walletService.deposit(userId, body.amount);
  }

  @Post(':userId/withdraw')
  withdraw(
    @Param('userId', ParseIntPipe) userId: number,
    @Body() body: AmountDto,
  ) {
    return this.walletService.withdraw(userId, body.amount);
  }

  @Get(':userId/balance')
  async getBalance(@Param('userId', ParseIntPipe) userId: number) {
    return { userId, balance: await this.walletService.getBalance(userId) };
  }
}
