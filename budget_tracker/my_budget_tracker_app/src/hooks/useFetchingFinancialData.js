import { useState, useEffect, useCallback } from 'react';
import axiosInstance from '../api/axiosApi';
import pLimit from 'p-limit';

export function useFetchingFinancialData(year, month) {
    const [data, setData] = useState({ incomes: [], expenses: [], creditCardExpenses: [] });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchYearData = useCallback(async (year) => {
        const params = new URLSearchParams({ year, include_recurring: true }).toString();
        const [incomeResponse, expenseResponse, creditCardResponse] = await Promise.all([
            axiosInstance.get(`incomes/?${params}`),
            axiosInstance.get(`expenses/?${params}`),
            axiosInstance.get(`credit-card-expenses/?${params}`),
        ]);

        return {
            incomes: incomeResponse.data,
            expenses: expenseResponse.data,
            creditCardExpenses: creditCardResponse.data,
        };
    }, []);

    const fetchData = useCallback(async () => {
        setLoading(true);

        try {
            const limit = pLimit(5); // Limit concurrency to 5 requests at a time

            // Fetch current year data
            const currentYearData = await fetchYearData(year);

            // Determine the maximum number of installments
            const maxInstallments = currentYearData.expenses.reduce((max, expense) => {
                return Math.max(max, expense.installments || 0);
            }, 0);

            // Determine the number of past years to fetch based on the maximum installments
            const yearsToFetch = Math.ceil(maxInstallments / 12);

            let pastDataResults = [];
            if (yearsToFetch > 0) {
                const pastYears = [];
                for (let i = 1; i <= yearsToFetch; i++) {
                    pastYears.push(year - i);
                }

                const pastDataPromises = pastYears.map((y) => limit(() => fetchYearData(y)));
                pastDataResults = await Promise.all(pastDataPromises);
            }

            // Combine past data with current data and avoid duplicates
            const allIncomes = mergeData(currentYearData.incomes, pastDataResults.flatMap(res => res.incomes || []));
            const allExpenses = mergeData(currentYearData.expenses, pastDataResults.flatMap(res => res.expenses || []));
            const allCreditCardExpenses = mergeData(currentYearData.creditCardExpenses, pastDataResults.flatMap(res => res.creditCardExpenses || []));

            setData({
                incomes: allIncomes,
                expenses: allExpenses,
                creditCardExpenses: allCreditCardExpenses,
            });

        } catch (error) {
            console.error('Failed to fetch financial data:', error);
            setError(error);
        } finally {
            setLoading(false);
        }
    }, [year, fetchYearData]);

    useEffect(() => {
        fetchData();
    }, [fetchData]);

    const mergeData = (currentData, pastData) => {
        const uniqueData = new Map();
        currentData.forEach(item => uniqueData.set(item.id, item));
        pastData.forEach(item => {
            if (!uniqueData.has(item.id)) {
                uniqueData.set(item.id, item);
            }
        });
        return Array.from(uniqueData.values());
    };

    return { data, loading, error };
}
