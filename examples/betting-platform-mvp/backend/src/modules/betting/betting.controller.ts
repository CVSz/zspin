import { Body, Controller, Param, ParseIntPipe, Post } from '@nestjs/common';
import { IsIn, IsNumber, IsString, Min } from 'class-validator';
import { BettingService } from './betting.service';

class PlaceBetDto {
  @IsString()
  matchId!: string;

  @IsNumber()
  @Min(1.01)
  odds!: number;

  @IsNumber()
  @Min(1)
  amount!: number;
}

class SettleBetDto {
  @IsIn(['win', 'lose'])
  result!: 'win' | 'lose';
}

@Controller('betting')
export class BettingController {
  constructor(private readonly bettingService: BettingService) {}

  @Post(':userId/place')
  placeBet(
    @Param('userId', ParseIntPipe) userId: number,
    @Body() body: PlaceBetDto,
  ) {
    return this.bettingService.placeBet(userId, body.matchId, body.odds, body.amount);
  }

  @Post(':betId/settle')
  settleBet(
    @Param('betId', ParseIntPipe) betId: number,
    @Body() body: SettleBetDto,
  ) {
    return this.bettingService.settleBet(betId, body.result);
  }
}
