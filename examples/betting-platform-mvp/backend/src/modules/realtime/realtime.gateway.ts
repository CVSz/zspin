import {
  MessageBody,
  SubscribeMessage,
  WebSocketGateway,
  WebSocketServer,
} from '@nestjs/websockets';
import { Server } from 'socket.io';

@WebSocketGateway({ cors: true })
export class RealtimeGateway {
  @WebSocketServer()
  server!: Server;

  sendBalanceUpdate(userId: number, balance: number) {
    this.server.emit(`balance-${userId}`, { balance });
  }

  sendBetUpdate(userId: number, bet: unknown) {
    this.server.emit(`bet-${userId}`, bet);
  }

  @SubscribeMessage('ping')
  handlePing(@MessageBody() _data: string): string {
    return 'pong';
  }
}
