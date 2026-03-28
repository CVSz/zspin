import { Module } from '@nestjs/common';
import { AdminController } from './admin/admin.controller';
import { BettingController } from './betting/betting.controller';
import { BettingService } from './betting/betting.service';
import { RealtimeGateway } from './realtime/realtime.gateway';
import { UsersService } from './users/users.service';
import { WalletController } from './wallet/wallet.controller';
import { WalletService } from './wallet/wallet.service';

@Module({
  controllers: [WalletController, BettingController, AdminController],
  providers: [UsersService, WalletService, BettingService, RealtimeGateway],
})
export class AppModule {}
