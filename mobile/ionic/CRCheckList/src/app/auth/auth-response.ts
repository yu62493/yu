export interface AuthResponse {
    user: {
        id: number,
        emplno: string,
        password: string,
        last_modify_date: string,
        created: string,
        days_since_created: number
    }
}
