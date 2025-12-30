-- RLS Policies for running_articles table
-- Run this in Supabase SQL Editor or via MCP migration

-- Enable RLS (already enabled, but shown for reference)
ALTER TABLE running_articles ENABLE ROW LEVEL SECURITY;

-- Policy 1: Allow public read access
CREATE POLICY "Allow public read access" ON running_articles
FOR SELECT USING (true);

-- Policy 2: Allow public insert
CREATE POLICY "Allow public insert" ON running_articles
FOR INSERT WITH CHECK (true);

-- Policy 3: Allow public update
CREATE POLICY "Allow public update" ON running_articles
FOR UPDATE USING (true);

-- Policy 4: Allow public delete
CREATE POLICY "Allow public delete" ON running_articles
FOR DELETE USING (true);

-- Note: For production, consider more restrictive policies:
-- Example: Only allow users to modify their own articles
-- CREATE POLICY "Users can only modify own articles" ON running_articles
-- FOR ALL USING (auth.uid() = user_id);

