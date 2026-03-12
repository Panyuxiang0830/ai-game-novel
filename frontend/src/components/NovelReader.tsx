// frontend/src/components/NovelReader.tsx
import type { NovelProject } from '../stores/novelStore';
import ReactMarkdown from 'react-markdown';
import { useState } from 'react';

interface NovelReaderProps {
  novel: NovelProject;
  onGenerateChapter: (chapterNum: number) => void;
  isLoading: boolean;
}

export default function NovelReader({ novel, onGenerateChapter, isLoading }: NovelReaderProps) {
  const [currentChapter, setCurrentChapter] = useState<number | null>(null);

  return (
    <div className="bg-apocalypse-card border border-apocalypse-border rounded-lg p-6">
      <h2 className="text-2xl font-bold text-apocalypse-text mb-4">
        {novel.skeleton?.premise || '末世生存小说'}
      </h2>

      {/* 章节列表 */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-apocalypse-text mb-3">章节</h3>
        <div className="grid grid-cols-5 gap-2">
          {novel.chapters.map((chapter) => (
            <button
              key={chapter.chapter_num}
              onClick={() => setCurrentChapter(chapter.chapter_num)}
              disabled={chapter.status === 'pending'}
              className={`px-4 py-2 rounded-lg transition-all ${
                currentChapter === chapter.chapter_num
                  ? 'bg-apocalypse-warning text-black'
                  : chapter.status === 'completed'
                  ? 'bg-apocalypse-border text-apocalypse-text hover:bg-apocalypse-muted'
                  : 'bg-apocalypse-bg text-apocalypse-muted cursor-not-allowed'
              }`}
            >
              {chapter.chapter_num}
            </button>
          ))}
        </div>
      </div>

      {/* 章节内容 */}
      {currentChapter && (
        <div className="border-t border-apocalypse-border pt-6">
          <h3 className="text-xl font-bold text-apocalypse-text mb-4">
            {novel.chapters[currentChapter - 1]?.title}
          </h3>

          {novel.chapters[currentChapter - 1]?.status === 'completed' ? (
            <div className="prose prose-invert max-w-none">
              <ReactMarkdown>
                {novel.chapters[currentChapter - 1]?.content}
              </ReactMarkdown>
            </div>
          ) : (
            <div className="text-center py-12">
              <button
                onClick={() => onGenerateChapter(currentChapter)}
                disabled={isLoading}
                className="px-6 py-3 bg-apocalypse-warning text-black font-semibold
                           rounded-lg hover:bg-apocalypse-warning/80 disabled:opacity-50
                           disabled:cursor-not-allowed transition-colors"
              >
                {isLoading ? '生成中...' : '生成此章节'}
              </button>
            </div>
          )}

          {novel.chapters[currentChapter - 1]?.word_count > 0 && (
            <p className="text-sm text-apocalypse-muted mt-4">
              字数: {novel.chapters[currentChapter - 1]?.word_count}
            </p>
          )}
        </div>
      )}

      {/* 进度统计 */}
      <div className="mt-6 pt-6 border-t border-apocalypse-border">
        <div className="flex justify-between text-sm text-apocalypse-muted">
          <span>完成进度: {novel.chapters.filter(c => c.status === 'completed').length}/{novel.chapters.length}</span>
          <span>总字数: {novel.total_words}</span>
        </div>
        <div className="h-2 bg-apocalypse-bg rounded-full overflow-hidden mt-2">
          <div
            className="h-full bg-apocalypse-success transition-all duration-500"
            style={{
              width: `${(novel.chapters.filter(c => c.status === 'completed').length / novel.chapters.length) * 100}%`
            }}
          />
        </div>
      </div>
    </div>
  );
}
