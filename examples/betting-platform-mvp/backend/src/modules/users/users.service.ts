import { Injectable } from '@nestjs/common';

export type User = { id: number; email: string };

@Injectable()
export class UsersService {
  private readonly users: User[] = [
    { id: 1, email: 'alice@example.com' },
    { id: 2, email: 'bob@example.com' },
    { id: 3, email: 'charlie@example.com' },
  ];

  async findAll(): Promise<User[]> {
    return this.users;
  }
}
