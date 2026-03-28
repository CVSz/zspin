import { Controller, Get } from '@nestjs/common';
import { UsersService } from '../users/users.service';
import { WalletService } from '../wallet/wallet.service';

@Controller('admin')
export class AdminController {
  constructor(
    private readonly usersService: UsersService,
    private readonly walletService: WalletService,
  ) {}

  @Get('users')
  async getUsers() {
    const users = await this.usersService.findAll();

    return Promise.all(
      users.map(async (u) => ({
        ...u,
        balance: await this.walletService.getBalance(u.id),
      })),
    );
  }
}
